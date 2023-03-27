@tool
extends EditorPlugin


var dock

func _enter_tree():
	# Initialization of the plugin goes here.
	dock = preload("res://addons/gpdot/prompter.tscn").instantiate()
	add_control_to_bottom_panel(dock, "ChatGPT")


func _exit_tree():
	# Clean-up of the plugin goes here.
	remove_control_from_bottom_panel(dock)
	dock.free()
