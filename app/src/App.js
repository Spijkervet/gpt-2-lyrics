import React from 'react';

import ReactQuill from 'react-quill'; // ES6
import 'react-quill/dist/quill.snow.css'; // ES6

import QuillMention from 'quill-mention'

import 'bootstrap/dist/css/bootstrap.css';
import './App.css';



class MyComponent extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      date: new Date(),
      temperature: 0.7,
      length: 40,
      language: "nl",
      title: "Title",
      text: "",
      healthcheck: "Offline",
      status: "Ready"
    };

    this.changeTemperature = this.changeTemperature.bind(this)
    this.changeLength = this.changeLength.bind(this)
    this.ref = React.createRef();
    this.handleLanguage = this.handleLanguage.bind(this)

    this.quillRef = null;      // Quill instance
    this.reactQuillRef = null; // ReactQuill component
    this.generateText = this.generateText.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.setTitle = this.setTitle.bind(this)
    this.healthCheck = this.healthCheck.bind(this)

  }

  componentDidMount() {
    this.attachQuillRefs()
    this.healthCheck()
  }

  componentDidUpdate() {
    this.attachQuillRefs()
  }

  attachQuillRefs = () => {
    if (typeof this.reactQuillRef.getEditor !== 'function') return;
    this.quillRef = this.reactQuillRef.getEditor();
  }

  handleChange(value) {
    this.setState({ text: value })
  }

  changeTemperature(e) {
    this.setState({
      temperature: e.target.value
    })
  }

  changeLength(e) {
    this.setState({
      length: e.target.value
    })
  }

  handleLanguage(e) {
    this.setState({ language: e.target.value });
  }

  setTitle(e) {
    this.setState({ title: e.target.value })
  }

  formats = [
    'header', 'bold', 'italic', 'underline', 'strike', 'color', 'align', 'indent', 'mention'
  ]

  modules = {
    toolbar: {
      container: '#toolbar',  // Selector for toolbar container
    },
    keyboard: {
      bindings: {
        // This will overwrite the default binding also named 'tab'
        tab: {
          key: 9,
          handler: () => {
            console.log('tab')
            var text = this.quillRef.getText()
            console.log(text)
          }
        }
      }
    }
  }


  generateText() {
    const editor = this.reactQuillRef.getEditor();
    const unprivilegedEditor = this.reactQuillRef.makeUnprivilegedEditor(editor);
    // You may now use the unprivilegedEditor proxy methods
    var text = unprivilegedEditor.getText();

    var selection = editor.getSelection(true)

    text = text.substr(0, selection.index)
    text = this.state.title + "\n" + text

    this.state.status = "Generating..."
    return fetch("http://localhost:8000/gpt2_lyrics", {
      method: 'POST',
      // mode: 'no-cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'omit', // include, *same-origin, omit
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'prompt': text,
        'temperature': this.state.temperature,
        'length': this.state.length,
        'language': this.state.language
      }),
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *client
    })
      .then(response => response.json())
      .then((jsonData) => {

        var arr = []
        for (var i = 0; i < jsonData['lyrics'].length; i++) {
          var j = {}
          j['id'] = i + 1
          j['value'] = jsonData['lyrics'][i]
          this.quillRef.insertText(selection.index, j['value']);
          arr.push(j)
        }
        console.log(arr)
        this.state.status = "Ready"
      })
      .catch((error) => {
        console.error(error)
        this.state.status = "Server Error"
      })
  }

  healthCheck() {
    setTimeout(this.healthCheck, 2000)

    fetch("http://localhost:5000/health", {
      method: 'GET'
    })
      .then((response) => {
        if (response.ok) {
          this.setState({ healthcheck: "Online" })
        }
      })
      .catch((error) => {
        this.setState({ healthcheck: "Offline" })
      })

  }


  render() {
    return (
      <div>
        <div className="sliders">
          <div className="slider-container">
            <span className="slider-name">Lijpe slider</span>
            <small>{this.state.temperature}</small>
            <input className="slider" type="range" min="0" max="1" defaultValue={this.state.temperature} step="0.1" onChange={this.changeTemperature} />
          </div>
          <div className="slider-container">
            <span className="slider-name">Words</span>
            <small>{this.state.length}</small>
            <input className="slider" type="range" min="1" max="1000" defaultValue={this.state.length} step="20" onChange={this.changeLength} />
          </div>
          <div className="slider-container">
            <select id="lang" onChange={this.handleLanguage} value={this.state.language}>
            <option value="en">English</option>
            <option value="nl">Nederlands</option>
            </select>
          </div>
          <div className="slider-container">
            <span className="slider-name">Server</span>
            <span style={{color: 'green'}}>{this.state.healthcheck}</span>
          </div>
          <div className="slider-container">
          <span className="slider-name">Status</span>
          <span style={{color: 'orange'}}>{this.state.status}</span>
          </div>
        </div>
        <hr />


        <div id="toolbar">
          <span className="ql-formats">
            <button className="generate-button" onClick={this.generateText}>Generate</button>
          </span>
          <span className="ql-formats">
            <select className="ql-header">
              <option value="1">Heading 1</option>
              <option value="2">Heading 2</option>
              <option value="3">Heading 3</option>
              <option value="4">Heading 4</option>
              <option value="5">Heading 5</option>
              <option value="6">Heading 6</option>
              <option value="">Normal</option>
            </select>
          </span>
          <span className="ql-formats">
            <button className="ql-bold"></button>
            <button className="ql-italic"></button>
            <button className="ql-underline"></button>
            <button className="ql-strike"></button>
          </span>
          <span className="ql-formats">
            <button className="ql-align" value=""></button>
            <button className="ql-align" value="center"></button>
            <button className="ql-align" value="right"></button>
            <button className="ql-align" value="justify"></button>
          </span>
          <span className="ql-formats">
            <select className="ql-color"></select>
            <select className="ql-background"></select>
          </span>
          <span className="ql-formats">
            <button className="ql-blockquote"></button>
          </span>
        </div>


        <div className="title-container">
          <input className="title" value={this.state.title} onChange={this.setTitle}></input>
        </div>

        <ReactQuill value={this.state.text}
          onChange={this.handleChange}
          theme="snow"
          modules={this.modules}
          formats={this.formats}
          ref={(el) => { this.reactQuillRef = el }}>
        </ReactQuill>
      </div>
    )
  }
}


class App extends React.Component {

  constructor(props) {
    super(props);

  }

  componentDidMount() {

  }

  render() {

    return (
      <div className="App">
        <header className="App-header">
          <div className="page-inner">
            <MyComponent
            />
          </div>
        </header>
      </div>
    )
  }
}

export default App;
