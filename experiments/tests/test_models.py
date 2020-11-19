from django.test import TestCase

from experiments.models import Compound, Project, Experiment, LabPerson, Aparat


class CompoundModelsTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="abc_project")
        self.lab_person = LabPerson.objects.create(
            name="lab_person",
            lab_email="lab_person@admin.com"
        )
        self.aparat = Aparat.objects.create(
            name="aparat",
        )
        self.compound = Compound.objects.create(
            name="compound_test",
            mass=500,
            monoisotopic_mass=501,
            formula="C6H12O6",
            project=self.project
        )

    def tearDown(self):
        self.project.delete()
        self.lab_person.delete()
        self.aparat.delete()
        self.compound.delete()


    def test_compound_creation(self):
        compound_from_db = Compound.objects.get(name="compound_test")
        self.assertEqual(compound_from_db.mass, 500)
        self.assertEqual(compound_from_db.monoisotopic_mass, 501)
        self.assertEqual(compound_from_db.formula, "C6H12O6")

    def test_compound_experimental_data_transfer_from_experiment_model(self):
        data = {"Sp": 1.0, "HyWi_Bm": 2.0}
        experiment = Experiment.objects.create(
            compound=self.compound,
            lab_person=self.lab_person,
            aparat=self.aparat,
            final=True,
            experimental_results=data
        )
        compound_from_db = Compound.objects.get(name="compound_test")
        self.assertEqual(compound_from_db.experimental_parameters["Sp"], 1.0)
        self.assertEqual(compound_from_db.experimental_parameters["HyWi_Bm"], 2.0)
