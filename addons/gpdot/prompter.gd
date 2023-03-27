@tool
extends Control


var stdout := []
var thread = Thread.new()


func addNewChat(s: String, rich: bool):
	var chat  = Label.new()
	
	if rich:
		chat = RichTextLabel.new()
		chat.bbcode_enabled = true
		chat.fit_content    = true
		chat.scroll_active  = false
		
	chat.text = s
	get_node("ChatContainer/ChatFlowWrapper/Container").add_child(chat)


func addNewQuestion(s: String):
	addNewChat("You: " + s, false)
	thread.start(executeAnswer.bind(s))


func executeAnswer(s: String):
	OS.execute("python", ["addons\\gpdot\\chatgpt.py", s], stdout, true)
	call_deferred("addNewAnswer")
	return stdout[stdout.size() - 1]


func addNewAnswer():
	var result = thread.wait_to_finish()
	addNewChat("ChatGPT: " + result, true)


func _on_chat_line_edit_text_submitted(new_text):
	addNewQuestion(new_text)
	$ChatContainer/ChatLineEdit.text = ""
