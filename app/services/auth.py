@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required_fields = ['name', 'email', 'password']
        
        for field in required_fields:
            if field not in data:
                raise APIError(f'Missing required field: {field}', status_code=400)
        
        result = AuthService.register_user(data)
        logger.info(f"New user registered: {data['email']}")
        
        return jsonify(result), 201
    except APIError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise e

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        required_fields = ['email', 'password']
        
        for field in required_fields:
            if field not in data:
                raise APIError(f'Missing required field: {field}', status_code=400)
        
        result = AuthService.login_user(data)
        logger.info(f"User logged in: {data['email']}")
        
        return jsonify(result)
    except APIError as e:
        logger.warning(f"Login failed: {str(e)}")
        raise e

@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        })
    except Exception:
        return jsonify({
            'valid': False
        }), 401