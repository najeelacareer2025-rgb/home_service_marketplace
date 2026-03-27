import gradio as gr

def hello(name):
    return f"Hello {name}, welcome to my Home Services Marketplace!"

demo = gr.Interface(fn=hello, inputs="text", outputs="text")

if __name__ == "__main__":
    demo.launch(share=True)

