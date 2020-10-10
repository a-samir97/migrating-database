import React from 'react'
import { Modal, Button, Form, Input, Space } from 'antd';
import { notificationBase } from './Notification';

const axios = require('axios').default

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};


export class SearchModal extends React.Component {
 
    constructor(props){
        super(props)
        // states for this component
        this.state = {
            columns:this.props.columns,
            visible:false,
        }
    }


  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  disappearModal = () => {
    this.setState({
      visible:false,
    });
  };

  handleOk = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  handleCancel = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  onFinish = data => {

    // axios request to API
    axios.put(`http://127.0.0.1:5000/db/${this.props.tableName}/update`, data)
    .then(response=>{
      
        console.log(response)

        // create success notification
        notificationBase('success', 'Added Row', 'you added a new row successfully.');
        // to make modal unvisible
        this.disappearModal();
    })
    .catch(error => {
      console.log(error)
      // creata danger notification
      notificationBase('error', 'Add Row Error', 'the row doesnt not add to the database, please try again');

    })
  }

  render() {
      let columNames = []
      for (let i = 0; i < this.state.columns.length - 2; i++) {

          // to get primary key 
          if(i === 0){
          columNames.push(
              <Form.Item
              id={this.state.columns[i]['title']}
              key={ this.state.columns[i]['title'] }
              label={ this.state.columns[i]['title'] }
              name='primaryKey' 
              rules={[
              {
                  message: `Please input your ${this.state.columns[i]['title'] }!`,
              },
              ]}
          >
                  <Input />
          </Form.Item>
      )
          } else {
            columNames.push(
              <Form.Item
              key={ this.state.columns[i]['title'] }
              label={ this.state.columns[i]['title'] }
              name={ this.state.columns[i]['title'] }
              rules={[
              {
                  message: `Please input your ${this.state.columns[i]['title'] }!`,
              },
              ]}
              >
                      <Input />
              </Form.Item>
          )
        }
          
          
      }
    return (
    
       <Space>    
          <Button type="danger" onClick={this.showModal}>
            Search
          </Button>

          <Modal
            title="Search"
            visible={this.state.visible}
            onOk={this.handleOk}
            onCancel={this.handleCancel}
          >
              <Form
                  {...layout}
                  name="basic"
                  initialValues={{
                      remember: true,
                  }}
                  onFinish={this.onFinish}
                  >

                  { columNames }

                  <Form.Item {...tailLayout}>
                      <Button type="primary" htmlType="submit">
                      Search
                      </Button>
                  </Form.Item>
              </Form>
          </Modal>
        </Space>
    );
  }
}
