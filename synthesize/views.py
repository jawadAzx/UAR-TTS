from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import json
@csrf_exempt
# Create your views here.
def synthesize(request):
    if request.method == 'POST':
        modelFolder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'synthesize', 'model')
        configPath = "config.json"
        modelPath = "checkpoint_430000.pth"
        outPath = "test.wav"
        data = request.body.decode('utf-8')
        data = json.loads(data)
        text = data['text']
        try:
            os.system("tts --text " + text + " --config_path " + configPath + " --model_path " + modelPath + " --out_path " + outPath)
            with open(outPath, 'rb') as f:
                response = HttpResponse(f.read(), content_type='audio/wav')
                response['Content-Disposition'] = 'attachment; filename="test.wav"'
                os.remove(outPath)
            return response
        except:
            return HttpResponse("Error")
    else:
        return HttpResponse("Not a GET request")

        
