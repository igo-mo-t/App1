from app import Dealer

def test_new_dealer():
    """
    GIVEN a Dealer model
    WHEN a new Dealer is created
    THEN check the name and city fields are defined correctly
    """
    dealer = Dealer('Gif','Moscow','')
    assert dealer.name =='Gif'
    assert dealer.city == 'Moscow'
    # assert dealer.role == 'dealer'