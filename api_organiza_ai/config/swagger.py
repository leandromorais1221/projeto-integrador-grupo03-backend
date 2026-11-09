SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "API OrganizaAI",
        "description": "API para gerenciamento de finanças pessoais",
        "version": "1.0.0",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Informe o token no formato: Bearer <JWT>",
        }
    },
}