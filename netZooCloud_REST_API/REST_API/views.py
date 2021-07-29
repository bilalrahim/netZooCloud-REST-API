# Django imports.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# netZooPy imports.
from netZooPy.lioness import Lioness
from netZooPy.panda import Panda

# Helper libraries.
import numpy as np
import os


# Create your views here.

@csrf_exempt
def lioness(request):
    if request.method == 'POST':
        
        # Uploaded files are saved in FILES of the request.
        files = request.FILES
        # Saves uploaded files to Disk.
        save_file(files)

        # Returns a dict of all the arguments passed in as query string in url.
        arguments = request.GET
        
        return JsonResponse(run_lioness(arguments['alpha'], arguments['precision'], arguments['mode'], arguments['start']))

def save_file(dict_file):
    with open(os.path.join('saved_files',"ppi.txt"), 'wb+') as f:
        f.writelines(dict_file['ppi'])

    with open(os.path.join('saved_files',"motif.txt"), 'wb+') as f:
        f.writelines(dict_file['motif'])

    with open(os.path.join("saved_files", "exp.txt"), 'wb+') as f:
        f.writelines(dict_file['exp'])


def run_lioness(alpha, precision, mode, start):
    print(os.getcwd())
    panda_obj = Panda('saved_files/exp.txt',
            'saved_files/motif.txt', 'saved_files/ppi.txt', modeProcess=mode, alpha=float(alpha), precision=precision, remove_missing=False, 
                  keep_expression_matrix=True, save_memory=False)

    lioness_obj = Lioness(panda_obj, start=int(start), end=int(start))

    # Returns a pandas dateframe.
    lioness_df =lioness_obj.export_lioness_results
    
    # Renaming force column
    # By default lioness names column force as '0'.
    lioness_df.columns = ["tf", "gene", "force"]

    lioness_df = lioness_df.astype(({"force":np.double}))


    lioness_df["motif"] = 0

    res_dict = {"file": lioness_df.to_dict()}
    return res_dict