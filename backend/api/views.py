import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.contrib.auth import authenticate
from rest_framework import status
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from .models import UploadHistory


@api_view(['POST'])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    csv_file = request.FILES['file']
    file_path = default_storage.save(csv_file.name, csv_file)

    # Read CSV
    df = pd.read_csv(file_path)

    # Summary
    summary = {
        "total_records": len(df),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    # Save to DB
    UploadHistory.objects.create(
        filename=csv_file.name,
        total_records=summary["total_records"],
        avg_flowrate=summary["avg_flowrate"],
        avg_pressure=summary["avg_pressure"],
        avg_temperature=summary["avg_temperature"],
        type_distribution=summary["type_distribution"],
    )

    # Keep only last 5 entries
    if UploadHistory.objects.count() > 5:
        oldest = UploadHistory.objects.order_by("uploaded_at").first()
        oldest.delete()

    # Remove uploaded file
    os.remove(file_path)

    return Response({
        "message": "File processed successfully",
        "summary": summary,
    })

@api_view(['GET'])
def get_history(request):
    history = UploadHistory.objects.order_by("-uploaded_at")[:5]

    data = []
    for h in history:
        data.append({
            "filename": h.filename,
            "uploaded_at": h.uploaded_at,
            "total_records": h.total_records,
            "avg_flowrate": h.avg_flowrate,
            "avg_pressure": h.avg_pressure,
            "avg_temperature": h.avg_temperature,
            "type_distribution": h.type_distribution,
        })

    return Response({"history": data})

@api_view(['GET'])
def generate_pdf(request):
    latest = UploadHistory.objects.order_by('-uploaded_at').first()

    if not latest:
        return Response({"error": "No history available to generate PDF"}, status=400)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "Chemical Equipment Summary Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"File Name: {latest.filename}")
    pdf.drawString(50, 740, f"Uploaded At: {latest.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")

    pdf.drawString(50, 710, f"Total Records: {latest.total_records}")
    pdf.drawString(50, 690, f"Average Flowrate: {latest.avg_flowrate}")
    pdf.drawString(50, 670, f"Average Pressure: {latest.avg_pressure}")
    pdf.drawString(50, 650, f"Average Temperature: {latest.avg_temperature}")

    # Type Distribution
    pdf.drawString(50, 620, "Type Distribution:")
    y = 600
    for eq_type, count in latest.type_distribution.items():
        pdf.drawString(70, y, f"{eq_type}: {count}")
        y -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="report.pdf")

@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
