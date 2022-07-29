import { CreateCategoryUseCase } from '@gb/core/dist/application/category/use-cases';

export class CreateCategoryDto implements CreateCategoryUseCase.Input {
  name: string;
  description?: string;
  is_active?: boolean;
}
