from tkinter import *

from gene_essence_interface.database.initialize_database import initialize_database
from gene_essence_interface.pages.ChooseAnalysisType.ChooseAnalysisType import ChooseAnalysisType
from gene_essence_interface.pages.ChooseHowToReceiveTheResults.ChooseHowToReceiveTheResults import ChooseHowToReceiveTheResults
from gene_essence_interface.pages.ChooseMetrics.ChooseMetrics import ChooseMetrics
from gene_essence_interface.pages.ChooseModels.ChooseModels import ChooseModels
from gene_essence_interface.pages.ConfirmInformationFrame.ConfirmInformationFrame import ConfirmInformationFrame
from gene_essence_interface.pages.InformationProject.InformationProject import InformationProject
from gene_essence_interface.pages.PrepareDataset.PrepareDataset import PrepareDataset
from gene_essence_interface.pages.PrepareDataset.RunPreparation import RunPreparation
from gene_essence_interface.pages.RunAnalysis.RunAnalysis import RunAnalysis
from gene_essence_interface.pages.StartPage.StartPage import StartPage


class PageManager(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.data_to_analyze = None
        self.prepare_params = None
        self.project_type = None
        self.directory_path = None
        self.model_parameters = {}
        self.test_size = None
        self.csv_file_path = None
        self.model_file_path = None
        self.receipt_in = None
        self.receipt_type = None
        self.controller = parent
        self.project_name = None
        self.analyse_type = None
        self.models = None
        self.metrics = None
        self.pages = {}
        self.page_history = []

        for Page in (StartPage, ChooseAnalysisType, InformationProject, ChooseModels, ChooseMetrics,
                     ChooseHowToReceiveTheResults, ConfirmInformationFrame, RunAnalysis,
                     PrepareDataset, RunPreparation):
            page_name = Page.__name__
            page = Page(parent=self, controller=self)
            self.pages[page_name] = page
            page.pack(fill=BOTH, expand=True)

        self.show_page("StartPage")

    def start_new_analysis(self):
        pages_to_destroy = [
            "ChooseAnalysisType",
            "InformationProject",
            "ChooseModels",
            "ChooseMetrics",
            "ChooseHowToReceiveTheResults",
            "ConfirmInformationFrame",
            "RunAnalysis"
        ]

        for page_name in pages_to_destroy:
            if page_name in self.pages:
                self.pages[page_name].destroy()
                del self.pages[page_name]

        for Page in (ChooseAnalysisType, InformationProject, ChooseModels, ChooseMetrics,
                     ChooseHowToReceiveTheResults, ConfirmInformationFrame, RunAnalysis):
            page_name = Page.__name__
            if page_name not in self.pages:
                page = Page(parent=self, controller=self)
                self.pages[page_name] = page

        self.page_history = []
        initialize_database()

        self.show_page("ChooseAnalysisType")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[page_name]
        page.pack(fill=BOTH, expand=True)
        page.update_idletasks()
        if hasattr(page, 'on_show'):
            page.on_show()

        if self.page_history and self.page_history[-1] != page_name:
            self.page_history.append(page_name)
        elif not self.page_history:
            self.page_history.append(page_name)

    def go_back(self):
        if len(self.page_history) > 1:
            self.page_history.pop()
            previous_page = self.page_history[-1]
            self.show_page(previous_page)

    def set_data_to_analyze(self, data):
        self.data_to_analyze = data

    def get_data_to_analyze(self):
        return self.data_to_analyze

    def set_prepare_params(self, params):
        self.prepare_params = params

    def get_prepare_params(self):
        return self.prepare_params

    def set_project_type(self, name):
        self.project_type = name

    def get_project_type(self):
        return self.project_type

    def set_project_name(self, name):
        self.project_name = name

    def get_project_name(self):
        return self.project_name

    def set_analyse_type(self, analyse_type):
        self.analyse_type = analyse_type

    def get_analyse_type(self):
        return self.analyse_type

    def set_csv_file_path(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def get_csv_file_path(self):
        return self.csv_file_path

    def set_model_file_path(self, model_file_path):
        self.model_file_path = model_file_path

    def get_model_file_path(self):
        return self.model_file_path

    def set_models(self, models):
        self.models = models

    def get_models(self):
        return self.models

    def set_metrics(self, metrics):
        self.metrics = metrics

    def get_metrics(self):
        return self.metrics

    def set_receipt_type(self, receipt_type):
        self.receipt_type = receipt_type

    def get_receipt_type(self):
        return self.receipt_type

    def set_receipt_in(self, receipt_in):
        self.receipt_in = receipt_in

    def get_receipt_in(self):
        return self.receipt_in

    def set_directory_path(self, directory_path):
        self.directory_path = directory_path

    def get_directory_path(self):
        return self.directory_path

    def set_test_size(self, test_size):
        self.test_size = test_size

    def get_test_size(self):
        return self.test_size

    def set_model_parameters(self, model_parameters):
        self.model_parameters = model_parameters

    def get_model_parameters(self, model_name):
        return self.model_parameters.get(model_name, {})

    def get_all_model_parameters(self):
        return self.model_parameters

    def update_model_parameters(self, model_name, updated_parameters):
        if model_name in self.model_parameters:
            self.model_parameters[model_name].update(updated_parameters)
