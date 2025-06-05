from injector import Injector
from services import IServiceA, IServiceB, IServiceC
from configs import config1, config2


def demo(injector: Injector):
    print("---- New Request ----")
    a1 = injector.get_instance(IServiceA)
    a2 = injector.get_instance(IServiceA)
    print(f"A? {a1 is a2}")

    with injector.create_scope():
        b1 = injector.get_instance(IServiceB)
        b2 = injector.get_instance(IServiceB)
        print(f"B in scope? {b1 is b2}")

        c1 = injector.get_instance(IServiceC)
        c2 = injector.get_instance(IServiceC)
        print(f"C? {c1 is c2}")

        print(a1.do_a(), b1.do_b(), c1.do_c(), sep=" | ")


if __name__ == "__main__":
    print("== Config 1 ==")
    demo(config1)

    print("\n== Config 2 ==")
    demo(config2)
