prod:
	docker-compose -f production.yml up --build --force-recreate -d

prod-proxy:
	docker-compose -f proxy.yml up --build --force-recreate -d

down:
	docker-compose -f production.yml down

local:
	docker-compose -f local.yml up --build
