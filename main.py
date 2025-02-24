import streamlit as st
from pipeline import run_pipeline
import pandas as pd


def convert_df(df):
    """
    The function converts data frame to CSV used for download CSV data function
    """
    return df.to_csv(index=False).encode('utf-8')

def main():
    
    """
    Main function contains all the UI parts of the application
    """
    st.set_page_config(page_title="Text2SQL", layout="wide")
    st.title("💬 Text2SQL Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], str):
                st.write(message["content"])
            else:
                st.write(message["content"]["Summary"])

                with st.expander("See SQL"):
                    for i in message["content"]["SQL_queries"]:
                        st.write(i)
                        st.write()

                if not message["content"]["db_output"].empty:
                    with st.expander("See Table"):
                        st.write(message["content"]["db_output"])

    user_input = st.chat_input("Type your message...")
    
    # Simple upload button
    uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False, type=["csv"],label_visibility="collapsed")

    # Handle uploaded file
    uploaded_df = pd.DataFrame()

    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)

        if uploaded_df.shape[0] > 15:
            st.error("Model cannot process more than 15 rows!")

        if uploaded_df.shape[1] > 5:
            st.error("Model cannot process more than 5 columns!")

    # Process user input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show the message in display
        with st.chat_message("user"):
            st.write(user_input)

        # Concatenate DataFrame if necessary
        input_data = user_input
        if not uploaded_df.empty:
            if uploaded_df.shape[0] > 15:
                return "Sorry, model can't process data with more than 15 rows"
            if uploaded_df.shape[1] > 5:
                return "Sorry, model can't process data with more than 5 columns"
            input_data += "\n\n" + uploaded_df.to_string()

        # Get output through pipeline
        bot_response = run_pipeline(input_data)

        # Append the output message of bot in the message history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # show bot output
        with st.chat_message("assistant"):
            if isinstance(bot_response, str):
                st.write(bot_response)
            else:
                st.write(bot_response["Summary"])

                with st.expander("See SQL"):
                    for i in bot_response["SQL_queries"]:
                        st.write(i)
                        st.write()

                if not bot_response["db_output"].empty:
                    with st.expander("See Table"):
                        st.write(bot_response["db_output"])

if __name__ == "__main__":
    main()
