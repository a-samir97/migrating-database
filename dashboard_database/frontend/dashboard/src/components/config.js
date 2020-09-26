import { Form, Input, Button } from 'antd';
import React from 'react'
import { useHistory } from 'react-router-dom'

const axios = require('axios').default;
const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 8,
  },
};

const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};

const Config = () => {
    
    const history = useHistory();
    const onFinish = (values) => {
    console.log('Success:', values);
    // POST Method
    axios.post('http://127.0.0.1:5000/db/config', values)
    .then(function(response){
        console.log(response)

        history.push('/tables')
    })
    .catch(function (error){
        console.log(error)
    })
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  return (
    <Form
      {...layout}
      name="basic"
      initialValues={{
        remember: true,
      }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
        <h1>Database Configuration</h1>
        <hr></hr>
      <Form.Item
        label="Database Type"
        name="type"
        rules={[
          {
            required: true,
            message: 'Please input your database type!',
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Database User"
        name="user"
        rules={[
          {
            required: true,
            message: 'Please input your user!',
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Database Password"
        name="password"
        rules={[
          {
            required: true,
            message: 'Please input your database password!',
          },
        ]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item
        label="Database Host"
        name="host"
        rules={[
          {
            required: true,
            message: 'Please input your database host!',
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Database Name"
        name="database"
        rules={[
          {
            required: true,
            message: 'Please input your database name!',
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
      
    </Form>
  );
};

export default Config;
