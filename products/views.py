# products/views.py
import openpyxl
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json

from tasks.mixins import PermissionRequiredMixin
from .data_import_handling import DataImport
from .models import Product


class UploadProductsView(PermissionRequiredMixin, View):
    template_name_upload = 'products_upload.html'
    template_name_update = 'products_update.html'
    group_name = 'Update latest product prices fetched from distributor'

    def get(self, request, *args, **kwargs):
        context = {
            'task': self.group_name,
        }
        return render(request, self.template_name_upload, context)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file_input')
        try:
            # Load the workbook and get the active worksheet
            data_importer = DataImport(uploaded_file)
            # import the data
            data_importer.import_data()
            # format the sheet to show the user what was uploaded
            products = data_importer.sheet.to_dict(orient='records')
            column_names = data_importer.sheet.columns.tolist()

            # Pass the data to the context for rendering
            context = {
                'column_names': column_names,
                'products': products,
                'task': self.group_name,
                'uploaded_file': uploaded_file,
            }
            return render(request, self.template_name_update, context)

        except openpyxl.utils.exceptions.InvalidFileException:
            # Handle the case where the file is not a valid XLSX file
            context = {
                'task': self.group_name,
                'error': 'The uploaded file is not a valid XLSX file.',
            }
            return render(request, self.template_name_upload, context)

        except Exception as e:
            # Handle any other exceptions that may occur
            context = {
                'task': self.group_name,
                'error': f'An error occurred while processing the file: {str(e)}',
            }
            return render(request, self.template_name_upload, context)
