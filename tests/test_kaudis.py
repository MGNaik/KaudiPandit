from src.kaudis import KaudiSet, Kaudi, KaudiState

def test_kaudi_roll():
    test_kaudi_1 = Kaudi(up_prob=1.0)
    test_kaudi_1.roll()
    assert test_kaudi_1.state == KaudiState.UP
    test_kaudi_2 = Kaudi(up_prob=0.0)
    test_kaudi_2.roll()
    assert test_kaudi_2.state == KaudiState.DOWN
    test_kaudi_3 = Kaudi(up_prob=0.5)
    test_kaudi_3.roll()
    assert test_kaudi_3.state != KaudiState.NOT_ROLLED



def test_kaudiset_roll():
    test_kaudiset_1 = KaudiSet(up_prob_list=[1.0,0.0,0.0,0.0,0.0,0.0])
    test_kaudiset_1.roll()
    assert test_kaudiset_1.KaudiSetValue == 1
    test_kaudiset_2 = KaudiSet(up_prob_list=[1.0,1.0,0.0,0.0,0.0,0.0])
    test_kaudiset_2.roll()
    assert test_kaudiset_2.KaudiSetValue == 2
    test_kaudiset_3 = KaudiSet(up_prob_list=[1.0,1.0,1.0,0.0,0.0,0.0])
    test_kaudiset_3.roll()
    assert test_kaudiset_3.KaudiSetValue == 3
    test_kaudiset_4 = KaudiSet(up_prob_list=[1.0,1.0,1.0,1.0,0.0,0.0])
    test_kaudiset_4.roll()
    assert test_kaudiset_4.KaudiSetValue == 4
    test_kaudiset_5 = KaudiSet(up_prob_list=[1.0,1.0,1.0,1.0,1.0,0.0])
    test_kaudiset_5.roll()
    assert test_kaudiset_5.KaudiSetValue == 5
    test_kaudiset_6 = KaudiSet(up_prob_list=[1.0,1.0,1.0,1.0,1.0,1.0])
    test_kaudiset_6.roll()
    assert test_kaudiset_6.KaudiSetValue == 6
    test_kaudiset_7 = KaudiSet(up_prob_list=[0.0,0.0,0.0,0.0,0.0,0.0])
    test_kaudiset_7.roll()
    assert test_kaudiset_7.KaudiSetValue == 12
    for i in range(0,100):
        test_kaudiset_8 = KaudiSet(up_prob_list=[0.5,0.5,0.5,0.5,0.5,0.5])
        test_kaudiset_8.roll()
        print(f"Total: {test_kaudiset_8.KaudiSetValue}")
        assert test_kaudiset_8.KaudiSetValue in [1,2,3,4,5,6,12]
    