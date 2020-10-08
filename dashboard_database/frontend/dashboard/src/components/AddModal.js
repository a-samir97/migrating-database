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


export class AddModal extends React.Component {
 
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
  }

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

    axios.post(`http://127.0.0.1:5000/db/${this.props.tableName}/insert`, data)
    .then(response=>{
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
      for (let i = 1; i < this.state.columns.length - 2; i++) {
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
    return (
    
       <Space>    
          <Button type="primary" onClick={this.showModal}>
            Add New Row
          </Button>

          <Modal
            title="Add Row"
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
                      Create
                      </Button>
                  </Form.Item>
              </Form>
          </Modal>
        </Space>
    );
  }
}
