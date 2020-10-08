import { Select, Form, Input, Button } from 'antd';
import React from 'react'
import { useHistory } from 'react-router-dom'
import { notificationBase } from './Notification'

const { Option } = Select;

function onChange(value) {
  console.log(`selected ${value}`);
}

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
          history.push('/tables')
          notificationBase('success', 'Connection Sucess', 'database connected successfully.');
      })
      .catch(function (error){
        notificationBase('error', 'Error', 'can not connect to the database, please try again');
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
          <Select
          showSearch
          style={{ width: 200 }}
          placeholder="Select your database"
          onChange={onChange}
        >
          <Option value="postgres">postgres</Option>
          <Option value="mariadb">mariadb</Option>
          <Option value="mysql">mysql</Option>
        </Select>
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
