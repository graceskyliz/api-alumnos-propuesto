import boto3
import botocore

def lambda_handler(event, context):
    # Entrada (json)
    body = event.get('body') or {}
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'message': 'Faltan parámetros: tenant_id y alumno_id son obligatorios'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    try:
        table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            # Evita eliminación silenciosa si no existe
            ConditionExpression='attribute_exists(tenant_id) AND attribute_exists(alumno_id)'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {'statusCode': 404, 'message': 'Alumno no encontrado'}
        raise

    return {
        'statusCode': 200,
        'message': 'Alumno eliminado correctamente'
    }
