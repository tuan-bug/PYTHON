import Home from '~/pages/Home/Home';
import NotFoundPage from '~/pages/NotFoundPage/NotFoundPage';
import Order from '~/pages/Order/Order';

export const routes = [
  {
    path: '/',
    page: Home,
    isShowHeader: true,
  },
  {
    path: '/order',
    page: Order,
    isShowHeader: true,
  },

  {
    path: '*',
    page: NotFoundPage,
  },
];
