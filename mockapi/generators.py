from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # schema.schemes = ["https"] if request and request.is_secure() else ["http"]
        schema.schemes = ["http", "https"]  # Include both
        return schema
