from gui_interface.app import App

# TODO WIT, splashscreen 1
# if getattr(sys, "frozen", False):
#     import pyi_splash


if __name__ == "__main__":
    app = App()

    # # TODO WIT, splashscreen 1
    # if getattr(sys, "frozen", False):
    #     pyi_splash.close()

    app.mainloop()
