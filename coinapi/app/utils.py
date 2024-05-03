def verify_inputs(args):
    currency = args.get('currency')
    quote_currency = args.get('quote_currency')
    operation = args.get('operation')

    supported_currencies = ['USD', 'CAD', 'EUR', 'AUD', 'BTC', 'ETH', 'DOGE', 'ADA']

    # Check if currency and quote currency are supported
    if currency not in supported_currencies:
        return False, f"Currency '{currency}' is not supported."
    if quote_currency not in supported_currencies:
        return False, f"Quote currency '{quote_currency}' is not supported."

    # Check if operation is valid
    if operation not in ['above', 'under']:
        return False, "Operation must be 'above' or 'under'."

    return True, None
