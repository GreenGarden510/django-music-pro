from flask_restful import Resource, reqparse
from .models import Configuration
from .schemas import ConfigurationSchema
from mkondo.security import authorized_users
from sqlalchemy import exc

configuration_schema = ConfigurationSchema()
configuration_list_schema = ConfigurationSchema(many=True)

class ConfigurationListResource(Resource):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('key', type=str, required=True)
    parser.add_argument('value', type=str, required=True)

    @staticmethod
    @authorized_users(['SA', 'A', 'C', 'U', 'V'])
    def get():
        # get all the records
        records = Configuration.all()
        
        # serialize the output
        response = configuration_list_schema.dump(records)
        return {
            'success': True,
            'data': response
        }, 200

    @staticmethod
    @authorized_users(['SA'])
    def post():
        # parsing and validating data 
        payload = ConfigurationListResource.parser.parse_args()

        # converting the payload from json to object
        obj = configuration_schema.load(payload)

        # initializing a new model
        configuration = Configuration(**obj)

        try:
            configuration.save()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return {
                       'success': False,
                       'message': 'Something went wrong while saving the model'
            }, 500

        # preparing the response
        response = configuration_schema.dump(configuration)
        return {
                   'success': True,
                   'message': 'Slider created successfully',
                   'data': response
               }, 201

class ConfigurationResource(Resource):
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('value', type=str, required=True)

    @staticmethod
    @authorized_users(['SA'])
    def put(configuration_id):
        # parsing and validating data
        payload = ConfigurationResource.parser.parse_args()

        # finding a new instance
        configuration = Configuration.find(configuration_id)

        # checking if configuration exist and if not return
        if not configuration:
            return {
                       'success': False,
                       'message': 'Configuration not found.'
                   }, 404
        
        # changing the instance values
        configuration.value = payload['value']

        # persisting the changes to the database
        try:
            configuration.save()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return {
                       'success': False,
                       'message': 'Something went wrong while updating the model'
            }, 500

        # preparing the respones
        response = configuration_schema.dump(configuration)

        # returning the response
        return {
                   'success': True,
                   'message': 'Configuration updated successfully',
                   'data': response
               }, 200

    @staticmethod
    @authorized_users(['SA'])
    def delete(configuration_id):
        # loading the instance
        configuration = Configuration.find(configuration_id)
        
        # if configuration not found  return with an error
        if not configuration:
            return {
                       'success': False,
                       'message': 'Slider not found.'
                   }, 404

        # if configuration found delete it
        try:
            configuration.delete()
        except exc.SQLAlchemyError as e:
            logging.error(e)
            return {
                       'success': False,
                       'message': 'Something went wrong while deleting the model'
            }, 500

        # return the response
        return {
            'success': True,
            'message': 'Slider deleted successfully'
        }, 204
