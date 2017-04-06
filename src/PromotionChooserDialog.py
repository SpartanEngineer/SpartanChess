from tkinter import Toplevel, Button, Tk, OptionMenu, StringVar, Message, simpledialog

#Knight converts to N so that it isn't confused with 'King' which converts to 'K'
pieceNameToPieceLetterConv = {'Queen':'Q', 'Knight':'N', 'Rook':'R',
        'Bishop':'B'}

class PromotionChooserDialog(simpledialog.Dialog):
    def body(self, master):
        self.msg = Message(master, text='Choose a piece to promote to:')
        self.msg.pack()

        self.optionVar = StringVar(master)
        self.optionVar.set('Queen')
        self.optionMenu = OptionMenu(master, self.optionVar, 'Queen',
        'Knight', 'Rook', 'Bishop')
        self.optionMenu.pack()

        self.pieceLetter = '?'
        self.canceled = True

    def apply(self):
        self.pieceLetter = pieceNameToPieceLetterConv[self.optionVar.get()]
        self.canceled = False
