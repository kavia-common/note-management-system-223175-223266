from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note.
    Exposes tags as an array of strings externally while storing as a comma-separated string.
    """

    # Represent tags outwardly as a list[str]
    tags = serializers.ListField(
        child=serializers.CharField(allow_blank=False),
        allow_empty=True,
        required=False,
        help_text="List of tags; will be stored as a comma-separated string internally.",
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "tags",
            "archived",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert comma-separated tags -> list
        data["tags"] = instance.tag_list()
        return data

    def validate_tags(self, value):
        # Normalize and deduplicate while preserving order
        seen = set()
        normalized = []
        for tag in value or []:
            t = tag.strip()
            if not t:
                # skip blanks
                continue
            if t.lower() not in seen:
                seen.add(t.lower())
                normalized.append(t)
        return normalized

    def create(self, validated_data):
        tags_list = validated_data.pop("tags", [])
        validated_data["tags"] = ",".join(tags_list)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "tags" in validated_data:
            tags_list = validated_data.pop("tags") or []
            instance.tags = ",".join(tags_list)
        return super().update(instance, validated_data)
