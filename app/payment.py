from razorpay import PaymentLink

razorpay_client = PaymentLink(key='rzp_test_0a8hEE6FVkqQAL',secret='Ko2w3TykK8fzPdBb2FZ3DREs')

def create_payment_link(amount, currency,doc_id):
    """Create a payment link using Razorpay."""
    try:
        # Initialize the Razorpay client with your API key and secret
        print("test")                    
    except Exception as e:
        print(f"Error initializing Razorpay client: {e}")
        return None