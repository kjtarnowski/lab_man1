from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from experiments.models import Compound, Project, Experiment, LabPerson, Aparat, ExperimentType
from experiments.serializers import CompoundSerializer, ExperimentSerializer


class CompoundApiViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test", password="12test12", email="test@example.com")
        cls.user.save()
        cls.project = Project.objects.create(name="test_project")
        cls.aparat = Aparat.objects.create(
            name="aparat",
        )
        cls.experiment_type = ExperimentType.objects.create(
            name="test_experiment_type",
        )
        cls.names = ("compound_test1", "compound_test2", "compound_test3")
        cls.masses = (400, 500, 600)
        cls.monoisotopic_masses = (401, 501, 601)
        cls.formulas = ("C6H12O6", "C6H6", "C7H6O3")
        cls.compounds = [
            Compound.objects.create(
                name=cls.names[i],
                mass=cls.masses[i],
                monoisotopic_mass=cls.monoisotopic_masses[i],
                formula=cls.formulas[i],
                project=cls.project,
            )
            for i in range(3)
        ]
        cls.compound = cls.compounds[0]

    def test_can_browse_all_compounds(self):
        self.client.login(username='test', password='12test12')
        response = self.client.get(reverse("compound-list"))

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.compounds), len(response.data))

        for compound in self.compounds:
            self.assertIn(CompoundSerializer(instance=compound).data, response.data)

    def test_can_read_a_specific_compound(self):
        self.client.login(username='test', password='12test12')
        response = self.client.get(reverse("compound-detail", args=[self.compound.id]))

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(CompoundSerializer(instance=self.compound).data, response.data)

    def test_can_add_a_new_compound(self):
        payload = {
            "id": 4,
            "name": "test_name",
            "mass": 250,
            "monoisotopic_mass": 251,
            "formula": "C6H6",
            "comments": "-",
            # "experimental_parameters": null,
            "project": self.project.id,
        }

        self.client.login(username='test', password='12test12')
        response = self.client.post(reverse("compound-list"), payload)
        created_compound = Compound.objects.get(name=payload["name"])

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        for k, v in payload.items():
            if k != "project":
                self.assertEquals(v, response.data[k])
                self.assertEquals(v, getattr(created_compound, k))

    def test_can_edit_a_compound(self):
        compound = Compound.objects.create(
            name="test_modification",
            mass=self.masses[0],
            monoisotopic_mass=self.monoisotopic_masses[0],
            formula=self.formulas[0],
            project=self.project,
            comments="-",
        )

        payload = {"formula": "C6H5NH2", "comments": "modified"}

        self.client.login(username='test', password='12test12')
        response = self.client.patch(reverse("compound-detail", args=[compound.id]), data=payload, format="json")

        compound.refresh_from_db()

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        for k, v in payload.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(compound, k))

    def test_can_delete_a_compound(self):
        self.client.login(username='test', password='12test12')
        response = self.client.delete(reverse("compound-detail", args=[self.compound.id]))

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Compound.objects.filter(pk=self.compound.id))


class ExperimentApiViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(name="test_project")
        cls.user = get_user_model().objects.create_user(username="test", password="12test12", email="test@example.com")
        cls.user.save()
        cls.lab_person = LabPerson.objects.create(
            user=cls.user, lab_name="lab_person", lab_email="lab_person@admin.com"
        )
        cls.aparat = Aparat.objects.create(
            name="test_aparat",
        )
        cls.experiment_type = ExperimentType.objects.create(
            name="test_experiment_type",
        )
        names = ("compound_test1", "compound_test2", "compound_test3")
        masses = (400, 500, 600)
        monoisotopic_masses = (401, 501, 601)
        formulas = ("C6H12O6", "C6H6", "C7H6O3")
        cls.compounds = [
            Compound.objects.create(
                name=names[i],
                mass=masses[i],
                monoisotopic_mass=monoisotopic_masses[i],
                formula=formulas[i],
                project=cls.project,
            )
            for i in range(3)
        ]
        cls.experiments = [
            Experiment.objects.create(
                compound=cls.compounds[i],
                lab_person=cls.lab_person,
                aparat=cls.aparat,
                exptype=cls.experiment_type,
            )
            for i in range(3)
        ]
        cls.experiment = cls.experiments[0]

    def test_can_browse_all_experiments(self):
        self.client.login(username='test', password='12test12')
        response = self.client.get(reverse("experiment-list"))

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.compounds), len(response.data))

        for experiment in self.experiments:
            self.assertIn(ExperimentSerializer(instance=experiment).data, response.data)

    def test_can_read_a_specific_experiment(self):
        self.client.login(username='test', password='12test12')
        response = self.client.get(reverse("experiment-detail", args=[self.experiment.id]))

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(ExperimentSerializer(instance=self.experiment).data, response.data)

    def test_can_add_a_new_experiment(self):
        payload = {
            "id": 4,
            "comments": "-",
            "experiment_date": "2020-11-25",
            "progress": "TBD",
            # "final": true,
            "experimental_results": {"ARR": 0.88, "GATS2i": 0.953},
            "compound": self.compounds[0].id,
            "lab_person": self.lab_person.id,
            "aparat": self.aparat.id,
            "exptype": self.experiment_type.id,
        }

        self.client.login(username='test', password='12test12')
        response = self.client.post(reverse("experiment-list"), payload, format="json")
        created_experiment = Experiment.objects.get(id=payload["id"])

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        for k, v in payload.items():
            self.assertEquals(v, response.data[k])
            if k in ("id", "comments", "progress"):
                self.assertEquals(v, getattr(created_experiment, k))

    def test_can_edit_an_experiment(self):
        experiment = Experiment.objects.create(
            compound=self.compounds[1],
            lab_person=self.lab_person,
            aparat=self.aparat,
            exptype=self.experiment_type,
            comments="-",
            progress="TBD",
        )

        payload = {"comments": "modified", "progress": "UC"}

        self.client.login(username='test', password='12test12')
        response = self.client.patch(reverse("experiment-detail", args=[experiment.id]), data=payload, format="json")

        experiment.refresh_from_db()

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        for k, v in payload.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(experiment, k))

    def test_can_delete_a_experiment(self):
        self.client.login(username='test', password='12test12')
        response = self.client.delete(reverse("experiment-detail", args=[self.experiment.id]))

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Experiment.objects.filter(pk=self.experiment.id))
