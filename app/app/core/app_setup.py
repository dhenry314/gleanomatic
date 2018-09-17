from ..main import app, api

""
api.add_resource(res,
		 "/resource",
                 "/resource/<string:resID>",
                 methods=['GET','POST','DELETE'],
                 resource_class_kwargs={ 'config': config })

api.add_resource(caps,
				 "/capability",
                 "/capability/<string:capID>",
                 methods=['GET','POST','DELETE'],
                 resource_class_kwargs={ 'config': config })

api.add_resource(rs,
                 "/RS/<string:sourceNamespace>",
                 "/RS/<string:sourceNamespace>/<string:setNamespace>",
                 "/RS/<string:sourceNamespace>/<string:setNamespace>/<string:capability>",
                 methods=['GET'],
                 resource_class_kwargs={ 'config': config })

""
