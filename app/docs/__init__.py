"""
API Documentation for Arvora EcoQuest Platform
---
tags:
  - name: auth
    description: Authentication endpoints
  - name: learning
    description: Learning and educational endpoints
  - name: eco
    description: Environmental impact tracking endpoints
  - name: social
    description: Social interaction endpoints
  - name: analytics
    description: Analytics and progress tracking endpoints

securityDefinitions:
  Bearer:
    type: apiKey
    name: Authorization
    in: header
    description: JWT token for authentication

responses:
  UnauthorizedError:
    description: Access token is missing or invalid
    schema:
      type: object
      properties:
        status:
          type: string
          example: error
        message:
          type: string
          example: Unauthorized access
"""