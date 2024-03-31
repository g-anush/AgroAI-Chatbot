from openai import OpenAI
import streamlit as st
import time
def Farmer_assistant(query,client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
            {
                "role": "assistant",
                "content":"Chatbot specialized in agriculture which can even answer about crop disease with cure and any type of farming related rqueries (like cattle farming).Whenever user ask about crop price, latest news about news and weather and even about policies for the farmers search them on google and then provide summarize information to the user, also while fetching the data don't say wait for a moment instead you just wait for that moment and directly give the information. If user ask any query which is not related to agriculture then politely say that you are only here for solving query related to agriculture.Always greet the user and say goodbye or bye to the user.Don't say to the user to wait for the moment instead you can wait for that and then give the fetched information to the user. Give response in that language user ask query if the user say that they need response in a specified langauge then give them solution in that language otherwise in give the response in the english."
            },
            {
                "role": "user",
                "content": f"Give a powerfull solution of the {query} precisely and accurately ."
            }
        ]
    )
    return response


def decode_text(unicode_text):
  decoded_text =  unicode_text.encode('utf-8').decode('utf-8')
  return decoded_text

# not using flask i want to print this code in my 

def generate_response(user_input,client):
    response = Farmer_assistant(user_input,client)
    output =  response.choices[0].message.content
    answer = decode_text(output)
    return answer

# Function to stop the spinner, alert, or error message after 5 seconds
def stop(alert):
    if alert:
        start_time = time.time()
        while (time.time() - start_time) < 5:
            continue
        alert.empty()

# Function to check if the response contains waiting keywords
def check_for_waiting(text):
    waiting_keywords = ["just a moment", "please wait", "hold on", "wait a moment", "please hold"]
    for keyword in waiting_keywords:
        if keyword in text.lower():
            return True
    return False
# Streamlit app
def main():
    st.set_page_config(page_title="AgroAI Chatbot", page_icon="🌾", layout="wide", initial_sidebar_state="collapsed")
    st.title("AgroAI Chatbot 🌾🤖")
    
    
    openai_api_key = st.text_input("Enter your Openai API Key here:", type="password")
    st.caption("Declaration📜: I don't save your openai api key, it is just for generating response for you.")
    
    client = OpenAI(api_key=openai_api_key)
    if st.button("Submit"): 
        try:
            # Attempt to create a client to check API key validity
            r = generate_response("Greet me", client)                  
        except Exception as e:
                    # Handle other exceptions
            error = st.error(f"An unexpected error occurred: {e}")
            stop(error)
            return
        else: 
                    
            with st.chat_message("🤖"):
                st.markdown(r)
                #st.session_state.messages.append({"role": "🤖", "content": response})
                    
    # Validate inputs and generate response    
    if openai_api_key:
        # don't want to display the above form now
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # Text input for user messages
        if user_input := st.chat_input("Write your query:"):
            st.session_state.messages.append({"role": "👩‍🌾", "content": user_input})
            
            with st.chat_message("👩‍🌾"): 
                st.markdown(user_input)
            with st.spinner("🤖 AgroAI is typing..."):   
                try:
                    # Attempt to create a client to check API key validity
                    response = generate_response(user_input, client)                  
                except Exception as e:
                    # Handle other exceptions
                    error = st.error(f"An unexpected error occurred: {e}")
                    stop(error)
                    return
                else:
                    with st.chat_message("🤖"):
                        while check_for_waiting(response):
                            time.sleep(5)
                            response=generate_response(user_input,client)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "🤖", "content": response})

        
               
                       
                   
    with st.popover("Note:"):
        st.write("This chatbot is create by a beginner for the project purpose, so if you find any issue or have any suggestion then please let me know. I will try to improve it.")
    with st.sidebar:        
        # Display section for creating API key
        with st.expander("How to create an OpenAI API key?"):
            st.write("1. Go to the [OpenAI website](https://platform.openai.com/signup).")
            st.write("2. Sign up for an account or log in if you already have one.")
            st.write("3. Go to the API section and create a new API key.")
            st.write("4. Copy the API key and paste it in the webpage.")
        
        with st.expander("Feedback"):
            st.write("If you have any feedback or suggestions for improving the chatbot, please feel free to share them with me. Your input is valuable and will help me enhance the chatbot's performance.")
            st.write("[✉️ Send Feedback](mailto:anushgupta2001@gmail.com)")
            st.write("Thank you for your support! 🙏")


        # Display section for about the chatbot
        with st.expander("About AgroAI Chatbot"):
            st.write("AgroAI Chatbot is a conversational agent designed to help farmers with their agricultural queries. It uses the GPT-3.5 model from OpenAI to generate responses to user queries. The chatbot can provide information on crop diseases, farming techniques, crop prices, weather forecasts, and government policies for farmers. It is a valuable tool for farmers to get quick and accurate information on various agricultural topics.") 
        st.write("---")

        st.header("👩‍💻 **About the Creator**")
        st.write("Hello! I'm Anush Gupta, a passionate and dedicated individual with a strong interest in artificial intelligence, machine learning, and data science. With a background in computer science, I'm constantly exploring new technologies and seeking innovative solutions to complex problems. I created the AgroAI Chatbot as a project to showcase my skills and contribute to the agricultural community.")
        st.write("Let's connect to explore opportunities, share knowledge, and collaborate on exciting projects!")
       
        st.write("🔗 **Connect with Me:**")
        #st.write("[🌐 Portfolio](https://guptaanush.netlify.app/)") 
        st.write("[📧 Email](mailto: anushgupta2001@gmail.com)")
        st.write("[📝 LinkedIn](https://www.linkedin.com/in/anushgupta-iitbhu/)")

        
    # Display section to know about creator
        st.write("---")
      

    
     
if __name__ == '__main__':
    main()
