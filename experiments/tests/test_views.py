import csv
import io

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from experiments.models import Compound, Project, Experiment, LabPerson, Aparat, ExperimentType


class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class CompoundViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = Project.objects.create(name="abc_project")
        cls.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        cls.user.save()
        cls.lab_person = LabPerson.objects.create(
            user=cls.user,
            lab_name="lab_person",
            lab_email="lab_person@admin.com"
        )
        cls.aparat = Aparat.objects.create(
            name="aparat",
        )
        cls.compound = Compound.objects.create(
            name="compound_test",
            mass=500,
            monoisotopic_mass=501,
            formula="C6H12O6",
            project=cls.project
        )
        data = {"Sp": 1.0, "HyWi_Bm": 2.0}
        cls.experiment = Experiment.objects.create(
            compound=cls.compound,
            lab_person=cls.lab_person,
            aparat=cls.aparat,
            final=True,
            experimental_results=data
        )

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='test', password='12test12')
        response = self.client.get('/experiments/compoundList/')
        self.assertEqual(response.status_code, 200)

    def test_context_from_url_after_compound_model_creation(self):
        login = self.client.login(username='test', password='12test12')
        response = self.client.get('/experiments/compoundList/')
        self.assertTrue(response.context['tableFilter'].qs[0].name == "compound_test")
        self.assertTrue(response.context['tableFilter'].qs[0].mass == 500)
        self.assertTrue(response.context['tableFilter'].qs[0].formula == "C6H12O6")

    def test_context_from_url_after_creation_experiment_and_subsequent_data_transfer_from_experiment_to_compound(self):
        login = self.client.login(username='test', password='12test12')
        response = self.client.get('/experiments/compoundList/')
        self.assertTrue(response.context['tableFilter'].qs[0].experimental_parameters["Sp"] == 1.0)
        self.assertTrue(response.context['tableFilter'].qs[0].experimental_parameters["HyWi_Bm"] == 2.0)


class UploadCompoundViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = Project.objects.create(name="test_project")
        cls.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        cls.user.save()

    def test_compounds_file_uploading_saving_to_compound_model(self):
        compound_name = "test_upload"
        compound_mass = 600
        compound_monoisotopic_mass = 601
        compound_formula = "C6H6"
        text = f'''compound_name,compound_mass,compound_monoisotopic_mass,compound_formula,comments,project_name
{compound_name},{compound_mass},{compound_monoisotopic_mass},{compound_formula},test,test_project'''

        csv_file = SimpleUploadedFile("file.csv", text.encode())
        login = self.client.login(username='test', password='12test12')
        response = self.client.post('/experiments/uploadCompound', {'file': csv_file})
        compound_from_db = Compound.objects.get(name=compound_name)
        self.assertEqual(compound_from_db.mass, compound_mass)
        self.assertEqual(compound_from_db.monoisotopic_mass, compound_monoisotopic_mass)
        self.assertEqual(compound_from_db.formula, compound_formula)


class UploadExperimentsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = Project.objects.create(name="abc_project")
        cls.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        cls.user.save()
        cls.lab_person = LabPerson.objects.create(
            user=cls.user,
            lab_name="lab_person",
            lab_email="lab_person@admin.com"
        )
        cls.aparat = Aparat.objects.create(
            name="test_aparat",
        )
        cls.compound = Compound.objects.create(
            name="compound_test",
            mass=500,
            monoisotopic_mass=501,
            formula="C6H12O6",
            project=cls.project
        )
        cls.experiment_type = ExperimentType.objects.create(
            name="test_experiment_type",
        )

    def test_experiment_file_uploading_saving_to_experiment_model(self):
        compound_name = "compound_test"
        text = f'''compound,experiment_type,experiment_date,experimental_set,aparat,lab_person,progess,final,comments
{compound_name},test_experiment_type,2020-10-01,test_experimental_set,test_aparat,lab_person,TBD,False,-,'''

        csv_file = SimpleUploadedFile("file.csv", text.encode())
        login = self.client.login(username='test', password='12test12')
        response = self.client.post('/experiments/uploadExperiment', {'file': csv_file})
        compound_from_db = Compound.objects.get(name=compound_name)
        experiment_from_db = Experiment.objects.filter(compound=compound_from_db).last()
        self.assertEqual(experiment_from_db.exptype.name, "test_experiment_type")
        self.assertEqual(experiment_from_db.aparat.name, "test_aparat")
        self.assertEqual(experiment_from_db.experimental_set.name, "test_experimental_set")

    def test_experiment_file_uploading_saving_to_experiment_model_update_experimental_data(self):
        compound_name = "compound_test"
        text = f'''compound,experiment_type,experiment_date,experimental_set,aparat,lab_person,progess,final,comments
{compound_name},test_experiment_type,2020-10-01,test_experimental_set,test_aparat,lab_person,TBD,False,-,'''

        csv_file = SimpleUploadedFile("file.csv", text.encode())
        login = self.client.login(username='test', password='12test12')
        response = self.client.post('/experiments/uploadExperiment', {'file': csv_file})

        text_with_data = f'''compound,experiment_type,experiment_date,experimental_set,aparat,lab_person,progess,final,comments,Sp,HyWi_Bm
{compound_name},test_experiment_type,2020-10-01,test_experimental_set,test_aparat,lab_person,TBD,False,-,1,2'''

        csv_file_with_data = SimpleUploadedFile("file.csv", text_with_data.encode())
        response = self.client.post('/experiments/uploadExperiment', {'file': csv_file_with_data})

        compound_from_db = Compound.objects.get(name=compound_name)
        experiment_from_db = Experiment.objects.filter(compound=compound_from_db).last()
        self.assertEqual(experiment_from_db.experimental_results["Sp"],  1.0)
        self.assertEqual(experiment_from_db.experimental_results["HyWi_Bm"], 2.0)



