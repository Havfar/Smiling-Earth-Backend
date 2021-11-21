from django.db.models.query_utils import Q
from django.shortcuts import render
from rest_framework import generics, permissions, response, status
from teams.models import Member, Team

from emissions.models import Emission
from emissions.serializers import EmissionSerializer, UpdateEmissionSerializer


class UserEmission(generics.ListCreateAPIView, generics.UpdateAPIView):
    serializer_class = EmissionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Emission.objects.filter(Q(user=user))
        return queryset


class UpdateOrCreateUserEmission(generics.CreateAPIView):
    serializer_class = UpdateEmissionSerializer
    queryset = Emission.objects.all()

    def create(self, request, *args, **kwargs):
        emission_queryset = Emission.objects.filter(
            user=request.user, weekNo=request.data['weekNo'])

        emission_exist = emission_queryset.first()
        data = self.request.data

        if emission_exist:
            for emission in emission_queryset:
                if emission.isSourceTransport:
                    emission.emissions = data["emissions"][0]["emission"]
                else:
                    emission.emissions = data["emissions"][1]["emission"]
                emission.save()
            return response.Response(status=status.HTTP_200_OK, data={"message": "emission updated successfully"})
        else:
            transport_emission = Emission(
                user=self.request.user,
                month=data["month"],
                year=data["year"],
                weekNo=data["weekNo"],
                emissions=data["emissions"][0]["emission"],
                isSourceTransport=True)

            energy_emission = Emission(
                user=self.request.user,
                month=data["month"],
                year=data["year"],
                weekNo=data["weekNo"],
                emissions=data["emissions"][1]["emission"],
                isSourceTransport=False)
            Emission.objects.bulk_create([transport_emission, energy_emission])
            return response.Response(status=status.HTTP_200_OK, data={"message": "emission created successfully"})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(status=status.HTTP_200_OK, data={"message": "emission updated successfully"})

        else:
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"message": "failed", "details": serializer.errors})


class TeamEmissions(generics.ListAPIView):
    serializer_class = EmissionSerializer

    def get_queryset(self):
        team = Member.objects.filter(team=self.kwargs['pk'])
        members = [user.user for user in team]
        queryset = Emission.objects.filter(Q(user__in=members))
        return queryset
