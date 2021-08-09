import uvicorn
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from database.resolvers import queries, datetime_scalar, mutations
from tortoise.contrib.starlette import register_tortoise

# Define Schema (schema.gql)
type_defs = load_schema_from_path('schema.gql')

# Define resolvers for data storage and fetching
schema = make_executable_schema(type_defs, queries, mutations, datetime_scalar)

# Setup Starlette ASGI App and setup Tortoise ORM
app = Starlette(debug=True)
register_tortoise(
	app,
	config_file='src/config.json',
)
#GraphQL route
app.mount('/graphql', GraphQL(schema, debug=True))


# Run this with poetry (poetry run poe run)
if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=4001)