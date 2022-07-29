import { UpdateCategoryUseCase } from '@gb/core/dist/application/category/use-cases';

export class UpdateCategoryDto
  implements Omit<UpdateCategoryUseCase.Input, 'id'>
{
  name: string;
  description?: string;
  is_active?: boolean;
}
