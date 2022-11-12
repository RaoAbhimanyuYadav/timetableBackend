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


# class GroupSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Group
#         fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    teacher = ProfessorSerializer(many=False)
    year = YearSerializer(many=False)
    # group_set = GroupSerializer(many=True)

    class Meta:
        model = Subject
        fields = '__all__'
