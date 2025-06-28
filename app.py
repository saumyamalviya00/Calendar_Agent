from agents import main_agent
from swarm import Swarm
import streamlit as st

if __name__ == "__main__":
    swarm_client = Swarm()
    agent = main_agent
    
    st.title('Create A Calendar AI Agent')
    
    if 'message' not in st.session_state:
        st.session_state.message = []
        
    for message in st.session_state.message:
        with st.chat_message(message['role']) :
            st.markdown(message['content'])
        
    if prompt := st.chat_input("Enter your prompt here..."):
        st.session_state.message.append({"role": "user", "content": prompt})
        
        with st.chat_message('user',avtar= '👤'):
            st.markdown(prompt)
            
        with st.chat_message.append('ai',avtar='🤖'):
            #print ('session state message', st.session_state.message)
            response = swarm_client.run(
                agent = agent,
                debug = False,
                #messages =[{'role':'user','content':prompt}] ,
                messages = st.session_state.message    
            )
            st.markdown(response.messages[-1]['content'])
        st.session_state.message.append({'role': 'assistant', 'content': response.messages[-1]['content']})