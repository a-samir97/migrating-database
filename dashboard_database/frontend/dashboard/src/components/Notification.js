import {notification } from 'antd';

export const notificationBase = (type, operation, desc) => {
    notification[type]({
      message: operation,
      description: desc
    });
  };

