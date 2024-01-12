INFRASTRUCTURE_TOKEN := token

ifneq ("$(wildcard ../ucraft-infrastructure/.env)","")
    include ../ucraft-infrastructure/.env
    export
endif

get-external:
	curl -H "Authorization: token $(INFRASTRUCTURE_TOKEN)" \
         -L https://raw.githubusercontent.com/ucraft-com/ucraft-infrastructure/master/whitelabels/Makefile \
		 -o ./Makefile && \
	curl -H "Authorization: token $(INFRASTRUCTURE_TOKEN)" \
         -L https://raw.githubusercontent.com/ucraft-com/ucraft-infrastructure/master/whitelabels/services.json \
		 -o ./services.json
