
from pymongo.database import Database
from local_config import *
from fastapi.responses import JSONResponse
import requests
import hashlib, hmac
import mercadopago
from email.message import EmailMessage
import ssl
import smtplib
import qrcode
import io
from email.utils import make_msgid
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from urllib.request import Request, urlopen
from bson import ObjectId
import base64
from copy import deepcopy

#de prod de mi cuenta de test
sdk = mercadopago.SDK(MP_TOKEN)

class MpClass():
    def __init__(self, manifest='', id_pago='', estado_pago='', hash='', db=Database, external_reference="", quantity=0, 
                 valor_unidad=0, fecha_desc="", origen=None):
        self.manifest = manifest
        self.id_pago = id_pago
        self.estado_pago = estado_pago
        self.db = db
        self.hash = hash
        self.external_reference = external_reference
        self.quantity = quantity
        self.valor_unidad = valor_unidad
        self.fecha_desc = fecha_desc
        self.origen = origen

    def generar_pdf_con_qr(self, qr_image_bytes, logo_url, texto_final):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Fondo negro
        c.setFillColor(colors.black)
        c.rect(0, 0, width, height, fill=1)

        # --- Agregar borde violeta alrededor de todo ---

        box_width = 360  # ancho del recuadro
        lineas = texto_final.split('\n')
        texto_alto = len(lineas) * 22 + 20
        box_height = 120 + 200 + texto_alto + 60  # suma logo + qr + texto + márgenes

        x_box = (width - box_width) / 2
        y_box = height - 50 - box_height

        violeta = colors.HexColor("#8A2BE2")
        c.setStrokeColor(violeta)
        c.setLineWidth(3)
        c.rect(x_box, y_box, box_width, box_height, fill=0)

        # --- Fin borde ---

        y_cursor = height - 50  # margen superior (puede quedarse igual)

        # Logo
        try:
            req = Request(
                logo_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urlopen(req) as response:
                header_data = response.read()
            header_img = ImageReader(io.BytesIO(header_data))
            c.drawImage(header_img, (width - 120) / 2, height - 170, width=120, height=120, mask='auto')
            y_cursor -= 160
        except:
            pass  

        # QR
        qr_img = ImageReader(io.BytesIO(qr_image_bytes))
        c.drawImage(qr_img, (width - 200) / 2, y_cursor - 200, width=200, height=200, mask='auto')
        y_cursor -= 220

        # Texto
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.white)

        line_height = 22
        y_cursor -= 20 

        for i, linea in enumerate(lineas):
            linea = linea.strip()
            y_linea = y_cursor - (i * line_height)
            c.drawCentredString(width / 2, y_linea, linea)

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer.read()
    
    def enviarMail(self, ticket, fecha):
        email_sender="cintassueltastickets@gmail.com"
        email_receiver=ticket["email"]

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = "Cintas Sueltas Tickets. Tus entradas."

        qr = qrcode.make(str(ticket["_id"]))
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        qr_bytes = buffer.read()
        
        qr2 = qrcode.make(str(ticket["_id"]))
        buffer2 = io.BytesIO()
        qr2.save(buffer2, format="PNG")
        buffer2.seek(0)

        logo_url = "https://i.imgur.com/V7xxMHN.png"
        
        texto_final = f"""
            Cantidad de entradas: {ticket["cantidad"]}\n
            Importe abonado: ${ticket["importe_total"]}\n
            ID de transaccion: {ticket["id_pago"]}"""
        
        pdf_data = self.generar_pdf_con_qr(qr_image_bytes=qr_bytes, logo_url=logo_url, texto_final=texto_final)

        qr_cid = make_msgid(domain="smtp.gmail.com")[1:-1]  

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <img src="{logo_url}" alt="Logo" style="width: 150px; margin-bottom: 20px;">
            <h2>¡Acá están tus tickets para el <strong>{fecha["nombre_evento"]}</strong>!</h2>
            <p>Mostrá este código QR al ingresar al evento.</p>
            <img src="cid:{qr_cid}" alt="Ticket para el {fecha["nombre_evento"]}" style="margin-top: 20px; width: 200px;">
            <p>Tu nombre: {ticket["nombre"]}</p>
            <p>Cantidad de entradas: {ticket["cantidad"]}</p>
            <p>Importe abonado: ${ticket["importe_total"]}</p>
            <p>ID de transaccion: {ticket["id_pago"]}</p>

            <p style="margin-top: 30px; font-size: 12px; color: gray;">Gracias por ser parte de la fecha 🎶</p>
        </body>
        </html>
        """

        filename=f'TicketCintasSueltas{ticket["_id"]}.pdf'

        em.set_content(html)
        em.add_alternative(html, subtype='html')
        em.add_attachment(
            pdf_data,
            maintype='application',
            subtype='pdf',
            filename=filename
        )

        em.get_payload()[1].add_related(
            buffer2.read(),
            maintype='image',
            subtype='png',
            cid=qr_cid
        )

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, PASS_GOOGLE)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            
    def generarPreferencia(self):
        preference_data = {
            # 'binary_mode': True,
            # "expiration_date_from": yyyy-MM-dd'T'HH:mm:ssz, PENDIENTE DEFINIR LA EXPIRACION
            # "expiration_date_to": yyyy-MM-dd'T'HH:mm:ssz,
            "expires": True,
            "notification_url": "https://web-production-35ede.up.railway.app/tickets/mp-notificacion",
            "external_reference": self.external_reference, 
            "items": [
                {
                    "title": self.fecha_desc,
                    "quantity": self.quantity,
                    "unit_price": self.valor_unidad
                }
            ],
            "back_urls": {
                "success": "https://www.cintassueltas.com.ar/success",
                "failure": "https://www.cintassueltas.com.ar/error",
                "pending": "https://www.cintassueltas.com.ar/pend"
            },
            "auto_return": "approved"
            }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        return preference
    

    def modificarEstadoPago(self):
        modificar_estado = True
        query = { "external_reference": self.external_reference }

        collection = self.db.ticket
        fechacollec = self.db.fecha

        if self.origen:
            header = {"Authorization": "Bearer " + MP_TOKEN}
            url = "https://api.mercadopago.com/v1/payments/"

            pago_call = requests.get(f"{url}{self.id_pago}", headers=header)

            pago_response = pago_call.json()

            estado_mp = pago_response["status"]

            if self.estado_pago != estado_mp:
                return None

        nuevoEstado = { "$set": { "estado_pago": self.estado_pago, "id_pago": self.id_pago } }

        estado_anterior_pago = collection.find_one(query)

        if estado_anterior_pago and estado_anterior_pago["estado_pago"] == "approved":
            modificar_estado = False
        
        query_fecha = {"_id": ObjectId(estado_anterior_pago["id_fecha"])}
                   
        fecha = fechacollec.find_one(query_fecha)

        ticket_copy = deepcopy(estado_anterior_pago)
        ticket_copy["_id"] = str(estado_anterior_pago["_id"])
        fecha["_id"] = str(fecha["_id"])

        qr = qrcode.make(ticket_copy["_id"])
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        qr_bytes = buffer.read()

        qr_base64 = base64.b64encode(qr_bytes).decode("utf-8")

        if modificar_estado:
            modificarAccion = collection.update_one(query, nuevoEstado)
            pago_act = collection.find_one(query)

            self.enviarMail(ticket=pago_act, fecha=fecha)

            if modificarAccion.modified_count > 0:
                return {"qr_code": qr_base64, "ticket": ticket_copy, "fecha": fecha}
            else:
                return {"qr_code": qr_base64, "ticket": ticket_copy, "fecha": fecha}
        else:
            return {"qr_code": qr_base64, "ticket": ticket_copy, "fecha": fecha}
                
    def notificacion(self):
        try:
            header = {"Authorization": "Bearer " + MP_TOKEN}
            url = "https://api.mercadopago.com/v1/payments/"

            pago_call = requests.get(f"{url}{self.id_pago}", headers=header)

            pago_response = pago_call.json()

            if "external_reference" in pago_response:
                external_reference = pago_response["external_reference"]
                self.external_reference = external_reference
                self.estado_pago = pago_response["status"]
                
                actualizar_estado = self.modificarEstadoPago()
        
                if actualizar_estado == 'Pago actualizado':
                    return JSONResponse(content={"Mensaje": actualizar_estado}, status_code=200)
                else:
                    return JSONResponse(content={"Mensaje": 'Error al actualizar estado'}, status_code=200)
            else:
                return {"Mensaje": "Pago no encontrado"}, 200
        except Exception as e:
            return JSONResponse(content={"Mensaje": str(e)}, status_code=400)
        
    def verificarToken(self):
        hmac_obj = hmac.new(MP_CLIENT_SECRET.encode(), msg=self.manifest.encode(), digestmod=hashlib.sha256)

        sha = hmac_obj.hexdigest()
        if sha == self.hash:
            return True
        else:
            return False