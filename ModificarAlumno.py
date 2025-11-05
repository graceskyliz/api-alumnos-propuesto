import boto3
import botocore

def lambda_handler(event, context):
    # Entrada (json)
    body = event.get('body') or {}
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    alumno_datos = body.get('alumno_datos')

    if not tenant_id or not alumno_id or alumno_datos is None:
        return {
            'statusCode': 400,
            'message': 'Faltan parámetros: tenant_id, alumno_id y alumno_datos son obligatorios'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    try:
        resp = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            # Actualiza todo el objeto alumno_datos (merge/replace a tu elección)
            UpdateExpression='SET alumno_datos = :datos',
            ExpressionAttributeValues={
                ':datos': alumno_datos
            },
            # Evita crear si no existe
            ConditionExpression='attribute_exists(tenant_id) AND attribute_exists(alumno_id)',
            ReturnValues='ALL_NEW'
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {'statusCode': 404, 'message': 'Alumno no existe'}
        raise

    return {
        'statusCode': 200,
        'alumno': resp.get('Attributes', {})
    }
