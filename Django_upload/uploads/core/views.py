from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from uploads.core.models import NN_Model

def simple_upload(request):
    if request.method == 'POST' and 'myfile' in request.FILES and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        model = NN_Model.get_instance()
        model.setup()
        results = model.predict(fs.path(filename))

        return render(request, 'core/simple_upload.html', {
            'results': results
        })

    return render(request, 'core/simple_upload.html')

