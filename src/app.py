import uvicorn
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from database.resolvers import queries, datetime_scalar, mutations
from tortoise.contrib.starlette import register_tortoise
from database import models

type_defs = load_schema_from_path('schema.gql')

schema = make_executable_schema(type_defs, queries, mutations, datetime_scalar)
app = Starlette(debug=True)
register_tortoise(
	app,
	config= {
		'connections': {
			'default': {
				'engine': 'tortoise.backends.asyncpg',
				'credentials': {
					'host': 'localhost',
					'port': '5432',
					'user': 'user',
					'password': 'resu',
					'database': 'test',
				}
			}
		},
		'apps': {
			'app': {
				'models': ['database.models'],
				'default_connection': 'default'
			}
		},
		'use_tz': True,
		'timezone':'UTC',
	},
)
app.mount('/graphql', GraphQL(schema, debug=True))


if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=4001)