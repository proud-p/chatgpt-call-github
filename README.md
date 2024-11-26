# **GitHub Repository Query Tool Using ChatGPT API**

This project is a Python-based application that leverages OpenAI’s GPT-4 API and the GitHub GraphQL API to dynamically generate and execute queries based on user input. It allows users to search for repositories that match their descriptions, making it easy to explore specific GitHub projects programmatically.

Users can say what they want to find, or what they are interested in natural language and will be returned with a list of repositories that matches that query.

**Example question:** 
How do I show pretty shaders on the web?


**Example output:**
```
----------------------------------------
Name: infinite-webl-gallery
Owner: bizarro
URL: https://github.com/bizarro/infinite-webl-gallery
Description: Infinite Auto-Scrolling Gallery using WebGL and GLSL Shaders.
----------------------------------------
Name: webgl-fundamentals
Owner: gfxfundamentals
URL: https://github.com/gfxfundamentals/webgl-fundamentals
Description: WebGL lessons that start with the basics
----------------------------------------
Name: webassembly-webgl-shaders
Owner: DanRuta
URL: https://github.com/DanRuta/webassembly-webgl-shaders
Description: Demo project for using WebGL shaders in WebAssembly
----------------------------------------
Name: webgl-workshop
Owner: stackgl
URL: https://github.com/stackgl/webgl-workshop
Description: :mortar_board: The sequel to shader-school: Learn the WebGL API
----------------------------------------
Name: shader-doodle
Owner: halvves
URL: https://github.com/halvves/shader-doodle
Description: A friendly web-component for writing and rendering shaders.
----------------------------------------
Name: webgl-shader-examples
Owner: jagracar
URL: https://github.com/jagracar/webgl-shader-examples
Description: Some simple examples of WebGL shaders
----------------------------------------
Name: jam3-lesson-webgl-shader-threejs
Owner: Experience-Monks
URL: https://github.com/Experience-Monks/jam3-lesson-webgl-shader-threejs
Description: Using custom vertex and fragment shaders in ThreeJS
----------------------------------------
Name: webglstudio.js
Owner: jagenjo
URL: https://github.com/jagenjo/webglstudio.js
Description: A full open source 3D graphics editor in the browser, with scene editor, coding pad, graph editor, virtual file system, and many features more.
----------------------------------------
Name: jam3-lesson-webgl-shader-intro
Owner: Experience-Monks
URL: https://github.com/Experience-Monks/jam3-lesson-webgl-shader-intro
Description: A brief introduction to fragment shaders.
----------------------------------------
```

# **Demo**
<video src="images/demo.mp4" autoplay muted loop playsinline width="100%"></video>
---

## **Features**
- Converts natural language queries into precise GraphQL queries for the GitHub API.
- Automatically fetches repository details, including name, owner, URL, and description.
- Integrates with the Azure OpenAI GPT-4 API for natural language understanding.
- Supports dynamic function calls to streamline GitHub queries and responses.

---

## **Project Folder**
- *images/* - contains images for README
- *libs/* - contains main scripts
    - **bot.py** - main code for the bot that is shown on the demo
    - **chatgpt_query_gui.py** - A small GUI application that helps you form your ChatGPT API function call JSON easily as shown below:
    ![Screenshot showing a small GUI application that helps you form your ChatGPT API function call](images/make_chatgpt_query_app.png)
-*notebooks/* - Notebooks to test code.


## **Setup Instructions**

### **Prerequisites**
1. Python 3.8+ installed on your machine.
2. An Azure OpenAI API key and endpoint.
3. A GitHub Personal Access Token. You can get your Personal Access Token like the picture shown below:
    ![Screenshot showing how to get personal access token on Github](images/github_auth.png)


### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/proud-p/chatgpt-call-github
   cd chatgpt-call-github
   ```
2. ```pip install -r requirements.txt```
3. Create a .env file in the root director with the following keys:
    ```
    AZURE_KEY=your_azure_openai_key
    AZURE_ENDPOINT=your_azure_openai_endpoint
    GITHUB_TOKEN=your_github_personal_access_token
    ```


## **Future Improvements**

GitHub is a powerful resource for developers, but querying it effectively can be a challenge. Learning the GitHub API or mastering advanced search operators isn't beginner-friendly, and simply typing into the search bar often yields suboptimal results due to the lack of natural language comprehension. This tool bridges the gap, enabling even beginners to search GitHub repositories effectively using natural language.

### **Why This Tool Matters**
- **Lowering the Barrier for Beginners**: By allowing users to input natural language queries, this tool makes GitHub's vast repository of knowledge accessible to everyone, not just seasoned developers.
- **Enhanced Search Precision**: The integration of GPT-4 enables more intelligent and context-aware searches compared to GitHub's standard search bar.

### **Planned Future Improvements**
1. **User-Friendly Interfaces**:
   - Develop a graphical user interface (GUI) or a web interface to make the tool even more accessible.
   - Allow users to input queries and view results in a visually appealing and structured format, rather than raw terminal output.

2. **Enhanced Output Formatting**:
   - Present search results in a structured table or JSON viewer, either in the terminal or a GUI.
   - Include clickable links, repository stats (stars, forks), and other metadata.

3. **Query Suggestions**:
   - Use GPT-4 to suggest or autocomplete queries based on partial inputs or common use cases.
   - Provide search tips or related queries to improve user exploration.

4. **Bookmarking and History**:
   - Allow users to save searches or bookmark repositories for easy reference later.
   - Maintain a history of queries and results for better continuity.

5. **Interactive Query Refinement**:
   - Allow users to refine their searches interactively by adding or removing filters through a conversational interface.

6. **Extended API Integration**:
   - Support additional GitHub features such as querying issues, pull requests, or even generating repository summaries.
   - Integrate with other APIs (e.g., GitLab or Bitbucket) to expand usability.

7. **Performance Optimizations**:
   - Cache results to reduce repeated API calls.
   - Handle large datasets more efficiently.

8. **Deployment as a Service**:
   - Host the tool as a web service so users can access it without setting up Python or APIs locally.
   - Include user authentication for private repository searches.

By addressing these improvements, this tool can evolve into a comprehensive solution for developers of all skill levels, transforming how they search and interact with GitHub's vast ecosystem.
