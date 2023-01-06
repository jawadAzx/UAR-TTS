from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import json
import subprocess
@csrf_exempt
# Create your views here.
def synthesize(request):
    if request.method == 'POST':
        configPath = "config.json"
        modelPath = "checkpoint_430000.pth"
        outPath = "test.wav"
        data = request.body.decode('utf-8')
        data = json.loads(data)
        text = data['text']
        command = "tts --text " + text + " --config_path " + configPath + " --model_path " + modelPath + " --out_path " + outPath
        venvActivate = "source /home/ubuntu/project/env/bin/activate"
        try:
            # make a subprocess call to the command and activate the virtual environment first to be used on ec2 instance
            subprocess.call(venvActivate + " && " + command, shell=True, executable='/bin/bash')
            with open(outPath, 'rb') as f:
                response = HttpResponse(f.read(), content_type='audio/wav')
                response['Content-Disposition'] = 'attachment; filename="test.wav"'
                os.remove(outPath)
            return response
        except:
            return HttpResponse("Error")
    else:
        return HttpResponse("Not a GET request")

        
