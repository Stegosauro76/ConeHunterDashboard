from django.shortcuts import render
import csv
import os
from django.http import JsonResponse
from django.conf import settings

def home(request):
    return render(request, 'cone_dashboard/dashboard.html')
def testing(request):
    return render(request, 'cone_dashboard/testing.html')

def training_results(request):
    return render(request, 'cone_dashboard/training_results.html')

def read_csv_data(file_path):
    data = []
    total_hours = 0
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            epoch = int(row['epoch'])
            co2 = float(row['co2'])
            training_hours = float(row.get('training_hours', 0))
            data.append({'epoch': epoch, 'co2': co2})
            total_hours += training_hours
    return data, round(total_hours, 2)

def co2_data_Yolo12(request):
    csv_path = os.path.join(settings.BASE_DIR, 'cone_dashboard', 'data', 'FasterCo2.csv')
    emissions = read_csv_data(csv_path)
    epochs=range(1,27)
    return JsonResponse({'data': emissions, 'epochs': epochs})

def co2_data_Faster(request):
    csv_path = os.path.join(settings.BASE_DIR, 'cone_dashboard', 'data', 'modelB.csv')
    data, total_hours = read_csv_data(csv_path)
    return JsonResponse({'data': data, 'totalTrainingHours': total_hours})

def metrics_data(request):
    faster = {
        'accuracy': 69.1, 'precision': 70, 'recall': 68,
        'f1_score': 90.6, 'mAp@0.5': 52.2, 'mAp@0.5:0.95':42.9
    }
    yolo = {
        'accuracy': 70.1, 'precision': 86.9, 'recall': 59,
        'f1_score': 89.5, 'mAp@0.5': 66.9, 'mAp@0.5:0.95':44.8
    }
    return JsonResponse({'yolo_metrics': yolo, 'faster_rcnn_metrics': faster})

# Aggiungi queste importazioni al tuo views.py
import os
import glob
from django.conf import settings


def yolo_images(request):
    """
    Restituisce le immagini/video dei risultati YOLO
    """
    # Percorso della cartella con le immagini YOLO
    yolo_images_path = os.path.join(settings.MEDIA_ROOT, 'yolo_results')
    
    # Crea la cartella se non esiste
    os.makedirs(yolo_images_path, exist_ok=True)
    
    images = []
    
    # Estensioni supportate
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.webm']
    
    # Cerca immagini
    for ext in image_extensions:
        for image_path in glob.glob(os.path.join(yolo_images_path, ext)):
            filename = os.path.basename(image_path)
            images.append({
                'title': filename.split('.')[0].replace('_', ' ').title(),
                'url': f"{settings.MEDIA_URL}yolo_results/{filename}",
                'type': 'image',
                'description': f'Risultato detection YOLO - {filename}'
            })
    
    # Cerca video
    for ext in video_extensions:
        for video_path in glob.glob(os.path.join(yolo_images_path, ext)):
            filename = os.path.basename(video_path)
            images.append({
                'title': filename.split('.')[0].replace('_', ' ').title(),
                'url': f"{settings.MEDIA_URL}yolo_results/{filename}",
                'type': 'video',
                'description': f'Video risultato YOLO - {filename}'
            })
    
    return JsonResponse({'images': images})

def faster_images(request):
    """
    Restituisce le immagini/video dei risultati Faster R-CNN
    """
    faster_images_path = os.path.join(settings.MEDIA_ROOT, 'faster_results')
  
    os.makedirs(faster_images_path, exist_ok=True)
    images = []
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.webm']
    for ext in image_extensions:
        for image_path in glob.glob(os.path.join(faster_images_path, ext)):
            filename = os.path.basename(image_path)
            images.append({
                'title': filename.split('.')[0].replace('_', ' ').title(),
                'url': f"{settings.MEDIA_URL}faster_results/{filename}",
                'type': 'image',
                'description': f'Risultato detection Faster R-CNN - {filename}'
            })

    for ext in video_extensions:
        for video_path in glob.glob(os.path.join(faster_images_path, ext)):
            filename = os.path.basename(video_path)
            images.append({
                'title': filename.split('.')[0].replace('_', ' ').title(),
                'url': f"{settings.MEDIA_URL}faster_results/{filename}",
                'type': 'video',
                'description': f'Video risultato Faster R-CNN - {filename}'
            })
    
    return JsonResponse({'images': images})


  