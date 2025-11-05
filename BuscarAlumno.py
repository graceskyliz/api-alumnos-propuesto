import boto3

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

    resp = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    item = resp.get('Item')

    if not item:
        return {'statusCode': 404, 'message': 'Alumno no encontrado'}

    return {
        'statusCode': 200,
        'alumno': item
    }
