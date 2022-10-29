from rest_framework import serializers

from timetable.models import Timing, Professor, Year, Subject


class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timing
        fields = '__all__'


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    # instructors = InstructorSerializer(many=True)

    class Meta:
        model = Subject
        fields = '__all__'
