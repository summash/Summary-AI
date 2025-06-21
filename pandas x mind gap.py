#summary ai
import tkinter as tk 
from tkinter import filedialog,messagebox
# =============================================================================
# from tkinterdnd2 import TkinterDnD, DND_FILES
# =============================================================================
from PIL import Image as img
import pytesseract as pt
import pdfplumber

#converting pdfs to texts 
def pdf_to_text(pdf_path):
    text= ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = text + page.extract_text() + "\n"
    return text        
    
#converting texts to summary
def text_to_summary(text: str) -> str:
    from transformers import pipeline

    summariser = pipeline("summarization", model="facebook/bart-large-cnn")
    text = text.replace("\n", " ")
    max_chunk = 1300

    # slice the text into chunks
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]

    partials = []
    for chunk in chunks:
        result = summariser(chunk,
                            max_length=150,
                            min_length=100,
                            do_sample=False)[0]["summary_text"]
        partials.append(result)

    combined = " ".join(partials).strip()

    # second pass if still long
    if len(combined) > max_chunk:
        combined = summariser(combined,
                              max_length=256,
                              min_length=120,
                              do_sample=False)[0]["summary_text"]
    return combined
            
#converting image to texts
def image_to_text(image_path):
    #load the image
    image = img.open(image_path)
    #ocr(optical character recognition) of the image
    text= pt.image_to_string(image)
    return text

#ui
class MyGUI:
    def __init__(self):
        #window
        self.root = tk.Tk()
        self.root.geometry("900x900")
        self.root.title("Summary AI")
        
        #drop image here
        #button
        self.pdf_btn = tk.Button(self.root,text="press here to upload pdf file",command=self.handle_pdf)
        self.img_btn = tk.Button(self.root,text="press here to upload your image",command=self.handle_img)
        self.summarize = tk.Button(self.root,text="summerize text",command=self.handle_summerization)
        self.img_btn.pack(pady=10)
        self.pdf_btn.pack(pady=10)
    
      
        self.summarize.pack(pady=10)
        
        
        #textbox
        self.input_text=tk.Text(self.root,height=20,width=100)
        self.input_text.pack(pady=10)
        
        self.summary_text = tk.Text(self.root,height=10,width=100,bg="lightyellow")
        self.summary_text.pack(pady=10)
        
        
        self.root.mainloop()
        

        #handle function
    def handle_img(self):
        filepath = filedialog.askopenfile(filetypes=[("image files","*.png *.jpeg* .jpg")],
                                          defaultextension=".png")
        if filepath:
            text = image_to_text(filepath)
            self.input_text.delete('1.0',tk.END)
            self.input_text.insert(tk.END,text)
           
        #drop pdf here 
    def handle_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files",".pdf")],
                                          defaultextension=".pdf")
        if filepath:
            text=pdf_to_text(filepath)
            self.input_text.delete('1.0',tk.END)
            self.input_text.insert(tk.END,text)
            
            
        #handle summarization
    def handle_summerization(self):
        original_text=self.input_text.get('1.0',tk.END)
        if not original_text.strip:
            messagebox.showwarning("Warning","No text to summarize")
            return
        summary = text_to_summary(original_text)
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert(tk.END, summary)
        
        
        
        


MyGUI()



















