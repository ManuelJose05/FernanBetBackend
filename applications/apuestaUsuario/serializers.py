from rest_framework import serializers
from .models import ApuestaUsuario, CondicionApuesta
from .utils import get_cuota_de_condicion
from ..match.models import Match
from ..player.models import Player


class CondicionApuestaSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(queryset=Player.objects.all(), required=False, allow_null=True)
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CondicionApuesta
        fields = [
            'id',
            'type',
            'match',
            'predicted_result',
            'player',
            'stat_type',
            'predicted_value',
        ]

    def validate(self, data):
        tipo = data.get('type')

        if tipo == 'player':
            if not data.get('player'):
                raise serializers.ValidationError({"player": "Este campo es requerido para apuestas de tipo jugador."})
            if not data.get('stat_type'):
                raise serializers.ValidationError({"stat_type": "Este campo es requerido para apuestas de tipo jugador."})
            if data.get('predicted_value') is None:
                raise serializers.ValidationError({"predicted_value": "Este campo es requerido para apuestas de tipo jugador."})

        elif tipo == 'match':
            if not data.get('match'):
                raise serializers.ValidationError({"match": "Este campo es requerido para apuestas de tipo partido."})
            if not data.get('predicted_result'):
                raise serializers.ValidationError({"predicted_result": "Este campo es requerido para apuestas de tipo partido."})

        else:
            raise serializers.ValidationError({"type": "Tipo de apuesta no válido."})

        return data

class ApuestaUsuarioSerializer(serializers.ModelSerializer):
    conditions = CondicionApuestaSerializer(many=True)
    ganancia_potencial = serializers.SerializerMethodField()

    class Meta:
        model = ApuestaUsuario
        fields = ['id', 'user', 'amount', 'ganancia_potencial','created_at', 'conditions']

    def create(self, validated_data):
        conditions_data = validated_data.pop('conditions')
        apuesta = ApuestaUsuario.objects.create(**validated_data)

        for cond_data in conditions_data:
            CondicionApuesta.objects.create(apuesta=apuesta, **cond_data)

        return apuesta

    def get_ganancia_potencial(self,obj):
        cuota = self.calcular_cuota(obj)
        return obj.amount * cuota

    def calcular_cuota(self,apuesta):
        conditions = apuesta.conditions.all()

        if not conditions:
            return 0

        total = 1

        for condition in conditions:
            total *= get_cuota_de_condicion(condition)
        return round(total,2)


